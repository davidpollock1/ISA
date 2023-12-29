import { NgModule } from '@angular/core';
import { Routes } from '@angular/router';
import { LayoutComponent } from './layout/layout.component';
import { HomeComponent } from './home/home.component';
import { SignInComponent } from './sign-in/sign-in.component';

const routeConfig: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      { path: '', component: HomeComponent },
      { path: 'sign-in', component: SignInComponent },
      // Add more routes as needed
    ]
  }
];

export default routeConfig;

