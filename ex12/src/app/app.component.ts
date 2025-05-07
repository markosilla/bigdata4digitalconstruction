import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import * as Papa from 'papaparse';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'ex12';
  chartOptions: any;

  constructor() {
    this.loadCSV();
  }

  loadCSV() {
    fetch('assets/706d79f84d75abd81744048179.csv')
        .then(res => res.text())
        .then(csv => {
          const parsed = Papa.parse(csv, { skipEmptyLines: true });
          const rows = parsed.data as string[][];

          const dataStart = rows.findIndex(row => /^\d{2}\.\d{2}\.\d{4}/.test(row[0]));
          const validRows = rows.slice(dataStart).filter(r => r.length >= 2);

          const data = validRows.map(row => {
            const [timestamp, rawConsumption] = row;
            const date = this.parseDate(timestamp);
            const day = date.toISOString().split('T')[0];
            const hour = date.toTimeString().slice(0, 5);
            const value = parseFloat(rawConsumption.replace(',', '.'));
            return { Day: day, Hour: hour, Consumption: value };
          });

          this.prepareChartData(data);
        });
  }

  parseDate(dateStr: string): Date {
    const [d, m, rest] = dateStr.split('.');
    const [y, h] = [rest.slice(0, 4), rest.slice(5)];
    return new Date(`${y}-${m}-${d}T${h}:00`);
  }

  prepareChartData(data: { Day: string; Hour: string; Consumption: number }[]) {
    const seriesMap: { [key: string]: { x: string; y: number }[] } = {};

    for (const row of data) {
      if (!seriesMap[row.Day]) {
        seriesMap[row.Day] = [];
      }
      seriesMap[row.Day].push({ x: row.Hour, y: row.Consumption });
    }

    const series = Object.entries(seriesMap).map(([name, data]) => ({ name, data }));

    this.chartOptions = {
      chart: {
        height: 350,
        type: "heatmap"
      },
      plotOptions: {
        heatmap: {
          shadeIntensity: 0.5,
          colorScale: {
            ranges: [
              { from: 0, to: 0.5, color: "#00A100", name: "Low" },
              { from: 0.5, to: 1.0, color: "#FFB200", name: "Medium" },
              { from: 1.0, to: 2.0, color: "#FF0000", name: "High" }
            ]
          }
        }
      },
      dataLabels: { enabled: false },
      series: series
    };
  }
}
