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

          // Find where the actual data starts
          const dataStart = rows.findIndex(row => /^\d{2}\.\d{2}\.\d{4}/.test(row[0]));
          const validRows = rows.slice(dataStart).filter(r => r.length >= 2);

          // Parse and convert the data
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

    // Sum up daily totals
    for (const row of data) {
      if (!dailyTotals[row.Day]) dailyTotals[row.Day] = 0;
      dailyTotals[row.Day] += row.Consumption;
    }

    // Group by month
    const monthMap: { [month: string]: { x: string; y: number }[] } = {};

    Object.entries(dailyTotals).forEach(([day, total]) => {
      const date = new Date(day);
      const month = date.toLocaleString('default', { month: 'short', year: 'numeric' });
      const dayOfMonth = date.getDate().toString();

      if (!monthMap[month]) monthMap[month] = [];
      monthMap[month].push({ x: dayOfMonth, y: parseFloat(total.toFixed(3)) });
    });

    const series = Object.entries(monthMap).map(([name, data]) => ({
      name,
      data
    }));

    this.chartOptions = {
      chart: {
        height: 450,
        type: "heatmap"
      },
      plotOptions: {
        heatmap: {
          shadeIntensity: 0.5,
          colorScale: {
            ranges: [
              { from: 0, to: 2, color: "#e0f7fa", name: "Low" },
              { from: 2, to: 5, color: "#80deea", name: "Medium" },
              { from: 5, to: 10, color: "#26c6da", name: "High" },
              { from: 10, to: 9999, color: "#006064", name: "Very High" }
            ]
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      xaxis: {
        title: { text: "Day of Month" }
      },
      series: series
    };
  }
}
