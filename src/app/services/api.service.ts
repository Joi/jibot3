import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
@Injectable({
	providedIn: 'root'
})
export class ApiService {
	constructor(
		private http: HttpClient,
	) { }
	public getApi = (url:string, options?:any):Observable<any> => this.http.get(url, options).pipe(catchError(this.apiError));
	private apiError = (error: HttpErrorResponse) => throwError(error);
}
