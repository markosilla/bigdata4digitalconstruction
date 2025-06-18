// src/app/app-routing.module.ts
import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {AuthGuard} from './auth.guard';
import {AppComponent} from './app.component';
import {GoogleSignInComponent} from './google-sign-in/google-sign-in.component';
import {DashboardComponent} from './dashboard/dashboard.component';

export const routes: Routes = [
  { path: 'login', component: GoogleSignInComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
