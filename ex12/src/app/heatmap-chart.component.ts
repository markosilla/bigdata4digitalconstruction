import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ApexAxisChartSeries, ApexChart, ApexDataLabels, ApexPlotOptions,
  ApexTooltip, ApexXAxis, ChartComponent, NgApexchartsModule
} from 'ng-apexcharts';
import * as Papa from 'papaparse';

export type ChartOptions = {
  chart: ApexChart;
  plotOptions: ApexPlotOptions;
  dataLabels: ApexDataLabels;
  tooltip: ApexTooltip;
  xaxis: ApexXAxis;
  series: ApexAxisChartSeries;
};

@Component({
  selector: 'heatmap-chart',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule],
  template: `
    <div style="width: 100%; margin: 0 auto; position: relative; padding: 150px 20px 20px;">
      <h1>
        1) Võta elektritarbimise aegridade andmebaasist (vt. Ülesanne 10) suvaline 1 andmestik ning proovi huvitaval moel visualiseerida neid andmeid nii, et saja päeva puhul hakkaksid "korduvad mustrid" "ilusti silma".
      </h1>

      <p>
        <strong>Selgitus:</strong> Elektritarbimise heatmap <code>706d79f84d75abd81744048179.csv</code> andmestiku põhjal — joonistuvad välja aastaaegadest kui ka nädalavahetuse päevadest sõltuvad mustrid (tõenäoliselt saunakerise kasutus on tihedam K, R, L, P).
      </p>
      <div id="chart" style="max-width: 100%; position: relative;">
        <apx-chart
          [series]="chartOptions.series"
          [chart]="chartOptions.chart"
          [plotOptions]="chartOptions.plotOptions"
          [dataLabels]="chartOptions.dataLabels"
          [tooltip]="chartOptions.tooltip"
          [xaxis]="chartOptions.xaxis"
        ></apx-chart>
      </div>
    </div>
  `
})
export class HeatmapChartComponent implements OnInit {
  @ViewChild("chart") chart!: ChartComponent;
  public chartOptions: ChartOptions;
  private static hourlyMap: Record<string, string> = {};

  constructor() {
    this.chartOptions = {
      chart: { height: 600, type: 'heatmap' },
      plotOptions: {} as ApexPlotOptions,
      dataLabels: { enabled: false },
      tooltip: {} as ApexTooltip,
      xaxis: { labels: { show: false } },
      series: [{ name: 'Loading...', data: [] }] as unknown as ApexAxisChartSeries
    };
  }

  ngOnInit() {
    this.loadCSV();
  }

  loadCSV() {
    fetch('/706d79f84d75abd81744048179.csv')
      .then(res => res.text())
      .then(csv => {
        const parsed = Papa.parse(csv, { skipEmptyLines: true, delimiter: ';' });
        const rows = parsed.data as string[][];
        const dataStart = rows.findIndex(row => row.length >= 2 && /^\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}$/.test(row[0]));
        const validRows = rows.slice(dataStart).filter(r => r.length >= 2);
        const directValues: Map<string, Map<number, string>> = new Map();

        validRows.forEach(row => {
          const [timestamp, consumption] = row;
          const [datePart, timePart] = timestamp.split(' ');
          const [hourPart] = timePart.split(':');
          const hour = parseInt(hourPart, 10);
          const [day, month, year] = datePart.split('.');
          const dayKey = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
          if (!directValues.has(dayKey)) directValues.set(dayKey, new Map());
          directValues.get(dayKey)!.set(hour, consumption);
        });

        const processedData = [];
        for (const [day, hourMap] of directValues.entries()) {
          const date = new Date(day);
          for (const [hour, valueStr] of hourMap.entries()) {
            const value = parseFloat(valueStr.replace(',', '.'));
            processedData.push({ day, date: new Date(date.getFullYear(), date.getMonth(), date.getDate(), hour), hour, value, displayValue: valueStr });
          }
        }

        this.prepareChartData(processedData, directValues);
      });
  }

  formatIntegerRange(value: number): string {
    return Math.round(value).toString();
  }

  prepareChartData(data: any[], directValues: Map<string, Map<number, string>>) {
    const dailyTotals: Record<string, number> = {};
    const hourlyBreakdown: Record<string, Array<string>> = {};
    HeatmapChartComponent.hourlyMap = {};

    const uniqueDays = [...new Set(data.map(item => item.day))];
    uniqueDays.forEach(day => {
      const dayData = data.filter(item => item.day === day);
      dailyTotals[day] = dayData.reduce((total, item) => total + item.value, 0);

      hourlyBreakdown[day] = Array(24).fill('0,000');
      const hourMap = directValues.get(day);
      if (hourMap) {
        for (let hour = 0; hour < 24; hour++) {
          if (hourMap.has(hour)) {
            hourlyBreakdown[day][hour] = hourMap.get(hour)!;
          }
        }
      }
    });

    const values = Object.values(dailyTotals);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const stepSize = range / 4;
    const colorScale = ["#00A100", "#128FD9", "#FFB200", "#FF0000"];
    const autoRanges = Array.from({ length: 4 }, (_, i) => {
      const from = min + i * stepSize;
      const to = i === 3 ? max + 1 : from + stepSize;
      return {
        from,
        to,
        color: colorScale[i],
        name: `${this.formatIntegerRange(from)}–${this.formatIntegerRange(to)}`
      };
    });

    const monthMap: { [month: string]: { x: string; y: number }[] } = {};

    Object.entries(dailyTotals).forEach(([day, total]) => {
      const date = new Date(day);
      const weekdayLabels = ["P", "E", "T", "K", "N", "R", "L"];
      const estDay = weekdayLabels[date.getDay()];
      const month = date.toLocaleString('default', { month: 'short', year: 'numeric' });
      const fullDateLabel = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
      const hours = hourlyBreakdown[day];
      const tooltipLabel = `${estDay}, ${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`;

      HeatmapChartComponent.hourlyMap[fullDateLabel] = `
        <table style="width:100%; font-size:12px;">
          <tr><td colspan="2" style="text-align:center; font-weight: bold;">${tooltipLabel}</td></tr>
          ${hours.map((val, hour) => `<tr><td>${hour.toString().padStart(2, '0')}:00</td><td style="text-align:right;">${val}</td></tr>`).join('')}
        </table>
      `;

      if (!monthMap[month]) {
        monthMap[month] = [];
      }
      monthMap[month].push({ x: fullDateLabel, y: total });
    });

    const series = Object.entries(monthMap).map(([name, data]) => ({ name, data }));

    const tooltipCustom = (info: any) => {
      const point = info.w.config.series[info.seriesIndex].data[info.dataPointIndex];
      const label = point.x;
      const total = point.y;
      const formattedTotal = typeof total === 'number' ? total.toFixed(3).replace('.', ',') : total;
      const hourly = HeatmapChartComponent.hourlyMap[label] || 'Andmed puuduvad';

      return `
        <div style="padding: 12px; width: 170px; background: #fff; border-radius: 5px;">
          <div style="margin-bottom: 10px;">Päeva kogutarbimine: <strong>${formattedTotal}</strong></div>
          ${hourly}
        </div>
      `;
    };

    this.chartOptions = {
      chart: { height: 900, type: 'heatmap', toolbar: { show: false } },
      plotOptions: {
        heatmap: {
          shadeIntensity: 0,
          distributed: true,
          colorScale: { ranges: autoRanges }
        }
      },
      dataLabels: {
        enabled: true,
        formatter: (_, opts) => {
          const pointDateStr = opts.w.config.series[opts.seriesIndex].data[opts.dataPointIndex].x;
          const pointDate = new Date(pointDateStr);
          const weekdayLabels = ["P", "E", "T", "K", "N", "R", "L"];
          return weekdayLabels[pointDate.getDay()];
        },
        style: { colors: ['#000'], fontSize: '14px', fontWeight: 'bold' }
      },
      tooltip: {
        custom: tooltipCustom,
        followCursor: true,
        x: { show: false },
        marker: { show: false }
      },
      xaxis: { labels: { show: false } },
      series: series
    };
  }
}
