import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ApexAxisChartSeries, ApexChart, ApexXAxis,
  ApexTooltip, ApexStroke, NgApexchartsModule
} from 'ng-apexcharts';
import * as Papa from 'papaparse';

export type ChartOptions = {
  chart: ApexChart;
  xaxis: ApexXAxis;
  tooltip: ApexTooltip;
  stroke: ApexStroke;
  series: ApexAxisChartSeries;
};

@Component({
  selector: 'multi-file-line-chart',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule],
  template: `
    <div style="padding: 100px 20px;">
      <h1>
        2) Võta elektritarbimise aegridade andmebaasist (vt. Ülesanne 10) palju andmestikke ning proovi huvitaval moel visualiseerida kõigi nende andmestike sama päeva nii,et "korduvad mustrid" hakkaksid "ilusti silma"
      </h1>

      <p>
        <strong>Selgitus:</strong> Ühe päeva tarbimine tunni kaupa ({{ TARGET_DATE }}) failidest:
        '706d79f84d75abd81744048179.csv',
        '0c3b30cd247fe6ff1742854250.csv',
        '1fecd574c4e953d91743336917.csv',
        '9ded8e1571c970631743483828.csv',
        '6f9be12993e8e64a1742388290.csv',
        '9e9dca492a061e211740838882.csv'. Lisaks keskmine tarbimine kõikidest andmestikest.
      </p>
      <apx-chart
        *ngIf="multiFileChartOptions.chart"
        [series]="multiFileLineSeries"
        [chart]="multiFileChartOptions.chart!"
        [xaxis]="multiFileChartOptions.xaxis!"
        [tooltip]="multiFileChartOptions.tooltip!"
        [stroke]="multiFileChartOptions.stroke!"
      ></apx-chart>
    </div>
  `
})
export class MultiFileLineChartComponent implements OnInit {
  readonly TARGET_DATE = '15.06.2024';
  public multiFileLineSeries: ApexAxisChartSeries = [];
  public multiFileChartOptions: Partial<ChartOptions> = {
    chart: {
      type: 'line',
      height: 600,
      zoom: { enabled: true },
      toolbar: { show: false }
    },
    xaxis: {
      categories: Array.from({ length: 24 }, (_, i) => `${i.toString().padStart(2, '0')}:00`),
      title: { text: 'Tund', style: { fontSize: '16px' } },
      labels: {
        rotate: -45,
        style: { fontSize: '12px' }
      }
    },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: (val) => val?.toFixed(3).replace('.', ',') + ' kWh'
      }
    },
    stroke: {
      width: 3,
      curve: 'smooth'
    }
  };

  ngOnInit() {
    const files = [
      '/706d79f84d75abd81744048179.csv',
      '/0c3b30cd247fe6ff1742854250.csv',
      '/1fecd574c4e953d91743336917.csv',
      '/9ded8e1571c970631743483828.csv',
      '/6f9be12993e8e64a1742388290.csv',
      '/9e9dca492a061e211740838882.csv'
    ];
    this.loadMultipleCSVs(files);
  }

  loadMultipleCSVs(filePaths: string[]) {
    const promises = filePaths.map(path =>
      fetch(path)
        .then(res => res.text())
        .then(csv => {
          const parsed = Papa.parse(csv, {
            skipEmptyLines: true,
            delimiter: ';'
          });

          const rows = parsed.data as string[][];
          const dataStart = rows.findIndex(row =>
            row.length >= 2 && /^\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}$/.test(row[0])
          );

          if (dataStart === -1) return null;

          const validRows = rows.slice(dataStart).filter(r => r.length >= 2);
          const hourlyValues: number[] = Array(24).fill(0);
          const filename = path.split('/').pop() || 'Fail';
          let foundData = false;

          for (const [timestamp, consumption] of validRows) {
            const [dateStr, timeStr] = timestamp.split(' ');
            if (dateStr !== this.TARGET_DATE) continue;

            const [hourStr] = timeStr.split(':');
            const hour = parseInt(hourStr, 10);
            const parsed = parseFloat(consumption.replace(',', '.'));
            if (hour >= 0 && hour < 24 && !isNaN(parsed)) {
              hourlyValues[hour] = parsed;
              foundData = true;
            }
          }

          if (!foundData) return null;

          return {
            name: `${filename}`,
            data: hourlyValues
          };
        })
    );

    Promise.all(promises).then(seriesList => {
      const validSeries = seriesList.filter(s => s !== null) as ApexAxisChartSeries;

      const averageValues: number[] = Array(24).fill(0);
      const counts: number[] = Array(24).fill(0);

      validSeries.forEach(series => {
        series.data.forEach((val, hour) => {
          if (typeof val === 'number' && !isNaN(val)) {
            averageValues[hour] += val;
            counts[hour]++;
          }
        });
      });

      for (let i = 0; i < 24; i++) {
        averageValues[i] = counts[i] > 0 ? averageValues[i] / counts[i] : 0;
      }

      const colorPalette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
        '#bcbd22', '#17becf', '#00b894', '#6c5ce7',
        '#fdcb6e', '#e17055'
      ];

      const coloredSeries = validSeries.map((series, i) => ({
        ...series,
        color: colorPalette[i % colorPalette.length]
      }));

      this.multiFileLineSeries = [
        ...coloredSeries,
        {
          name: `Keskmine (${this.TARGET_DATE})`,
          data: averageValues,
          color: '#000000'
        }
      ];
    });
  }
}
