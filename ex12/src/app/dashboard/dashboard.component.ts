import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HeatmapChartComponent} from '../heatmap-chart.component';
import {MultiFileLineChartComponent} from '../multi-file-line-chart.component';
import {AuthService} from '../auth.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [
    CommonModule,
    HeatmapChartComponent,
    MultiFileLineChartComponent
  ],
  template: `
    <button (click)="logout()">Logout</button>
    <heatmap-chart></heatmap-chart>
    <multi-file-line-chart></multi-file-line-chart>
  `
})
export class DashboardComponent {

  constructor(private authService: AuthService, private router: Router) { }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
