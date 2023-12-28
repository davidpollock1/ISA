import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module'; // Import AppModule

const platform = platformBrowserDynamic();

platform.bootstrapModule(AppModule)
  .catch(err => console.error(err));