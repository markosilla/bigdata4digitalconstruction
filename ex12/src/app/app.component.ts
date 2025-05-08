import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeatmapChartComponent } from './heatmap-chart.component';
import { MultiFileLineChartComponent } from './multi-file-line-chart.component'; // ✅ ensure this is imported

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    HeatmapChartComponent,
    MultiFileLineChartComponent // ✅ make sure it's in the imports array
  ],
  template: `
    <heatmap-chart></heatmap-chart>
    <multi-file-line-chart></multi-file-line-chart>
  `
})
export class AppComponent {}
