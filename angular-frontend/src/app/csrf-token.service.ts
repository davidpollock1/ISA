import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CsrfTokenService {

  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  async fetchCsrfToken(): Promise<void> {
    await this.http.get<any>(this.apiUrl + '/accounts/csrf_cookie/', { observe: 'response', withCredentials: true })
      .subscribe();
  }
}
