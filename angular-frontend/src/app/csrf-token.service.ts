import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CsrfTokenService {

  private apiUrl = '//localhost:8000'

  constructor(private http: HttpClient) { }
  

  async fetchCsrfToken(): Promise<void> {

    await this.http.get<any>(this.apiUrl + '/accounts/csrf_cookie', { observe: 'response', withCredentials: true })
    .subscribe();

  }
}
