// app.component.ts
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
    fetch('/706d79f84d75abd81744048179.csv')
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
            const value = parseFloat(rawConsumption.replace(',', '.'));
            return { Day: day, Consumption: value };
          });

          this.prepareChartData(data);
        });
  }

  parseDate(dateStr: string): Date {
    const [datePart, timePart] = dateStr.split(' ');
    const [day, month, year] = datePart.split('.');
    return new Date(`${year}-${month}-${day}T${timePart}:00`);
  }

  prepareChartData(data: { Day: string; Consumption: number }[]) {
    const dailyTotals: Record<string, number> = {};

    for (const row of data) {
      if (!dailyTotals[row.Day]) dailyTotals[row.Day] = 0;
      dailyTotals[row.Day] += row.Consumption;
    }

    const values = Object.values(dailyTotals);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;

    const colorSteps = 4;
    const stepSize = range / colorSteps;
    const colorScale = [
      "#00A100",
      "#128FD9",
      "#FFB200",
      "#FF0000"
    ];

    const autoRanges = Array.from({ length: colorSteps }, (_, i) => {
      const from = min + i * stepSize;
      const to = i === colorSteps - 1 ? max + 1 : from + stepSize;
      return {
        from: parseFloat(from.toFixed(2)),
        to: parseFloat(to.toFixed(2)),
        color: colorScale[i],
        name: `${from.toFixed(0)}–${to.toFixed(0)}`
      };
    });

    const weekdayLabels = ["P", "E", "T", "K", "N", "R", "L"];
    const monthMap: { [month: string]: { x: string; y: number }[] } = {};

    Object.entries(dailyTotals).forEach(([day, total]) => {
      const date = new Date(day);
      const weekday = date.getDay(); // 0 = Sunday, 6 = Saturday
      const estDay = weekdayLabels[weekday];
      const month = date.toLocaleString('default', { month: 'short', year: 'numeric' });
      const label = `${estDay}${date.getDate()}`;

      if (!monthMap[month]) monthMap[month] = [];
      monthMap[month].push({ x: label, y: parseFloat(total.toFixed(3)) });
    });

    const series = Object.entries(monthMap).map(([name, data]) => ({ name, data }));

    this.chartOptions = {
      chart: {
        height: 600,
        type: 'heatmap'
      },
      plotOptions: {
        heatmap: {
          shadeIntensity: 0,
          useFillColorAsStroke: false,
          distributed: false,
          colorScale: {
            ranges: autoRanges
          }
        }
      },
      dataLabels: { enabled: false },
      xaxis: {
        title: { text: 'Päev (E,T,K,N,R,L,P)' },
        labels: { style: { fontSize: '14px' } }
      },
      series: series
    };
  }
}
