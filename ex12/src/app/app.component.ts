import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {GoogleSignInComponent} from './google-sign-in/google-sign-in.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    GoogleSignInComponent,
  ],
  template: `
    <div class="page-container">
      <app-google-sign-in></app-google-sign-in>
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
