import { NgModule } from '@angular/core';
import { HomeComponent } from './home/home.component';
import { LayoutComponent } from './layout/layout.component';
import { HttpClientModule, HttpClientXsrfModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { BrowserModule } from '@angular/platform-browser';
import { NavbarComponent } from './navbar/navbar.component';
import routeConfig from './app.routes';
import { CsrfInterceptorService } from './csrf-interceptor.service';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LayoutComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: "csrftoken", // Adjust if needed
      headerName: "X-CSRFToken", // Adjust if needed
    }),
    RouterModule.forRoot(
      routeConfig),
    // ... other imports
  ],
  bootstrap: [AppComponent],
  providers: [
    // [
    //   { provide: HTTP_INTERCEPTORS, 
    //     useClass: CsrfInterceptorService, 
    //     multi: true }
    // ],
  ], // Add any app-wide providers here
})
export class AppModule {}