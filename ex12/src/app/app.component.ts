import {Component, OnInit, ViewChild} from '@angular/core';
import {CommonModule} from '@angular/common';
import {
  ApexAxisChartSeries,
  ApexChart,
  ApexDataLabels,
  ApexPlotOptions,
  ApexTooltip,
  ApexXAxis,
  ChartComponent,
  NgApexchartsModule
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
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule],
  template: `
    <div style="width: 100%; margin: 0 auto; position: relative; padding: 150px 20px 20px;">
      <h1>Elektritarbimise heatmap</h1>

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
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'ex12';

  @ViewChild("chart") chart!: ChartComponent;
  public chartOptions: ChartOptions;

  // Make hourlyMap static so it's accessible to the tooltip function
  private static hourlyMap: Record<string, string> = {};

  constructor() {
    this.chartOptions = {
      chart: {
        height: 600,
        type: 'heatmap'
      } as ApexChart,
      dataLabels: {
        enabled: false
      } as ApexDataLabels,
      plotOptions: {

      } as ApexPlotOptions,
      tooltip: {
        // Initialize with empty settings, will be set in prepareChartData
      } as ApexTooltip,
      xaxis: {
        labels: {
          show: false, // Hide x-axis labels by default
          style: { fontSize: '14px' }
        }
      } as ApexXAxis,
      series: [{
        name: 'Loading...',
        data: []
      }] as unknown as ApexAxisChartSeries
    };
  }

  ngOnInit() {
    this.loadCSV();
  }

  loadCSV() {
    fetch('/706d79f84d75abd81744048179.csv')
        .then(res => res.text())
        .then(csv => {
          // Parse with custom delimiter based on the format
          const parsed = Papa.parse(csv, {
            skipEmptyLines: true,
            delimiter: ';' // Set explicit delimiter as semicolon
          });

          const rows = parsed.data as string[][];

          // Find the data start by looking for date pattern
          const dataStart = rows.findIndex(row =>
              row.length >= 2 && /^\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}$/.test(row[0])
          );

          const validRows = rows.slice(dataStart).filter(r => r.length >= 2);

          // Create a map to directly store hourly values by day and hour
          const directValues: Map<string, Map<number, string>> = new Map();

          // Process each row and store the original value
          validRows.forEach(row => {
            const [timestamp, consumption] = row;

            // Extract date parts manually
            const [datePart, timePart] = timestamp.split(' ');
            const [hourPart] = timePart.split(':');
            const hour = parseInt(hourPart, 10);

            // Create a clean day key (YYYY-MM-DD)
            const [day, month, year] = datePart.split('.');
            const dayKey = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;

            // Store the direct value
            if (!directValues.has(dayKey)) {
              directValues.set(dayKey, new Map());
            }
            directValues.get(dayKey)!.set(hour, consumption);
          });

          // Now convert the direct data to our processing format
          const processedData = [];

          for (const [day, hourMap] of directValues.entries()) {
            const date = new Date(day);

            let dailyTotal = 0;
            for (const [hour, valueStr] of hourMap.entries()) {
              // Calculate daily total for the heatmap
              const value = parseFloat(valueStr.replace(',', '.'));
              dailyTotal += value;

              processedData.push({
                day,
                date: new Date(date.getFullYear(), date.getMonth(), date.getDate(), hour),
                hour,
                value,
                displayValue: valueStr
              });
            }
          }

          this.prepareChartData(processedData, directValues);
        })
        .catch(error => {
          console.error('Error loading CSV:', error);
        });
  }

  // Format integer ranges for the color scale
  formatIntegerRange(value: number): string {
    return Math.round(value).toString();
  }

  prepareChartData(
      data: { day: string; date: Date; hour: number; value: number; displayValue: string }[],
      directValues: Map<string, Map<number, string>>
  ) {
    // Calculate daily totals without processing the hourly values
    const dailyTotals: Record<string, number> = {};
    const hourlyBreakdown: Record<string, Array<string>> = {};
    AppComponent.hourlyMap = {}; // reset before rebuilding

    // First, create an array of unique days
    const uniqueDays = [...new Set(data.map(item => item.day))];

    // For each day, calculate the daily total and build the hourly breakdown
    uniqueDays.forEach(day => {
      // Get all hours for this day
      const dayData = data.filter(item => item.day === day);

      // Calculate daily total
      dailyTotals[day] = dayData.reduce((total, item) => total + item.value, 0);

      // Create hourly breakdown with DIRECT values
      hourlyBreakdown[day] = Array(24).fill('0,000');

      // Fill in direct values from the CSV
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

    const colorSteps = 4;
    const stepSize = range / colorSteps;
    const colorScale = ["#00A100", "#128FD9", "#FFB200", "#FF0000"];

    // Create integer-based ranges
    const autoRanges = Array.from({ length: colorSteps }, (_, i) => {
      const from = min + i * stepSize;
      const to = i === colorSteps - 1 ? max + 1 : from + stepSize;
      return {
        from: from,
        to: to,
        color: colorScale[i],
        name: `${this.formatIntegerRange(from)}–${this.formatIntegerRange(to)}`
      };
    });

    // Estonian weekday abbreviations
    const weekdayLabels = ["P", "E", "T", "K", "N", "R", "L"];
    const monthMap: { [month: string]: { x: string; y: number }[] } = {};

    Object.entries(dailyTotals).forEach(([day, total]) => {
      const date = new Date(day);
      const weekday = date.getDay(); // 0 = Sunday

      // Use only weekday abbreviation (E, T, K, N, R, L, P)
      const estDay = weekdayLabels[weekday];
      const month = date.toLocaleString('default', { month: 'short', year: 'numeric' });

      // Use only the weekday as label
      const label = estDay;

      const hours = hourlyBreakdown[day];

      // For tooltip, use complete date info
      const tooltipLabel = `${estDay}, ${date.getDate()}.${date.getMonth()+1}.${date.getFullYear()}`;

      // Create a table-like structure with DIRECT values from CSV
      AppComponent.hourlyMap[`${month}|${label}`] = `
        <table style="width:100%; font-size:12px; border-collapse: collapse;">
          <tr>
            <td colspan="2" style="text-align:center; padding-bottom: 8px; font-weight: bold;">
              ${tooltipLabel}
            </td>
          </tr>
          <tr style="border-bottom: 1px solid #ddd;">
            <th style="text-align:left; padding: 3px 0;">Tund</th>
            <th style="text-align:right; padding: 3px 0;">kWh</th>
          </tr>
          ${hours.map((val, hour) =>
          `<tr>
              <td style="padding: 2px 0">${hour.toString().padStart(2, '0')}:00</td>
              <td style="text-align:right; padding: 2px 0">${val}</td>
            </tr>`
      ).join('')}
        </table>
      `;

      if (!monthMap[month]) {
        monthMap[month] = [];
      }
      monthMap[month].push({
        x: label,
        y: total
      });
    });

    const series = Object.entries(monthMap).map(([name, data]) => ({
      name,
      data
    }));

    // Updated tooltipCustom function - larger with no scrollbars
    const tooltipCustom = function(info: any) {
      const seriesIndex = info.seriesIndex;
      const dataPointIndex = info.dataPointIndex;
      const w = info.w;

      const point = w.config.series[seriesIndex].data[dataPointIndex];
      const label = point.x;
      const seriesName = w.config.series[seriesIndex].name;
      const total = point.y;

      const key = `${seriesName}|${label}`;
      const hourly = AppComponent.hourlyMap[key] || 'Andmed puuduvad';

      // Format total with comma decimal separator
      let formattedTotal = String(total);
      if (typeof total === 'number') {
        formattedTotal = total.toFixed(3).replace('.', ',');
      }

      // Create a larger tooltip without scrollbars
      return `
        <div style="
          padding: 12px;
          width: 150px;
          background-color: #fff;
          border-radius: 5px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.15);
          overflow: visible;
        ">
          <div style="
            margin-bottom: 10px;
            font-size: 13px;
          ">Päeva kogutarbimine: <strong>${formattedTotal}</strong></div>

          <div style="max-height: none; overflow: visible;">
            ${hourly}
          </div>
        </div>
      `;
    };

    // Update chart options with the new data
    this.chartOptions = {
      chart: {
        height: 900,
        type: 'heatmap'
      } as ApexChart,
      plotOptions: {
        heatmap: {
          shadeIntensity: 0,
          useFillColorAsStroke: false,
          distributed: true,
          colorScale: {
            ranges: autoRanges
          }
        }
      } as ApexPlotOptions,
      dataLabels: {
        enabled: false
      } as ApexDataLabels,
      tooltip: {
        custom: tooltipCustom,
        // Make tooltip follow cursor completely
        followCursor: true,
        // Hide X indicator
        x: {
          show: false
        },
        // No fixed position
        fixed: {
          enabled: false
        },
        // Hide marker
        marker: {
          show: false
        }
      } as ApexTooltip,
      xaxis: {
        // Remove x-axis title and labels
        labels: {
          show: false  // Hide labels
        }
      } as ApexXAxis,
      series: series as unknown as ApexAxisChartSeries
    };
  }
}
