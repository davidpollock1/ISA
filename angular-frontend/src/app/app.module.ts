import { NgModule } from '@angular/core';
import { HomeComponent } from './home/home.component';
import { LayoutComponent } from './layout/layout.component';
import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi, withXsrfConfiguration } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { BrowserModule } from '@angular/platform-browser';
import { NavbarComponent } from './navbar/navbar.component';
import routeConfig from './app.routes';
import { DashboardComponent } from './dashboard/dashboard/dashboard.component';
import { FormsModule } from '@angular/forms';
import { BuilderComponent } from "./builder/builder.component";

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        LayoutComponent,
        NavbarComponent,
        DashboardComponent,
    ],
    bootstrap: [AppComponent], imports: [BrowserModule,
        FormsModule,
        RouterModule.forRoot(routeConfig), BuilderComponent], providers: [
            provideHttpClient(withInterceptorsFromDi(), withXsrfConfiguration({
                cookieName: "csrftoken",
                headerName: "X-CSRFToken",
            }))
        ]
})
export class AppModule { }