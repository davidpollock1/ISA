import { NgModule } from '@angular/core';
import { Routes } from '@angular/router';
import { LayoutComponent } from './layout/layout.component';
import { HomeComponent } from './home/home.component';
import { SignInComponent } from './sign-in/sign-in.component';
import { DashboardComponent } from './dashboard/dashboard/dashboard.component';

const routeConfig: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      { path: '', component: HomeComponent },
      { path: 'sign-in', component: SignInComponent },
      { path: 'dashboard', component: DashboardComponent}
      // Add more routes as needed
    ]
  }
];

export default routeConfig;

