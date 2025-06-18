import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
  ],
  template: `
    <div class="page-container">
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    .page-container {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 1rem;
      box-sizing: border-box;
    }
  `]
})
export class AppComponent {}
