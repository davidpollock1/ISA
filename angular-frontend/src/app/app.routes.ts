// app-routing.module.ts
import { NgModule } from '@angular/core';
import { Routes } from '@angular/router';
import { LayoutComponent } from './layout/layout.component';
import { HomeComponent } from './home/home.component';

const routeConfig: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      { path: '', component: HomeComponent },
      // Add more routes as needed
    ]
  }
];

export default routeConfig;

