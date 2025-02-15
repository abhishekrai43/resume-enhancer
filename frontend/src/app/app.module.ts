import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { appRoutes } from './app.routes'; // Ensure this file exists

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(withInterceptorsFromDi()), // Replaces HttpClientModule
    provideRouter(appRoutes)
  ]
}).catch(err => console.error(err));
