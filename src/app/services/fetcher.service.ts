import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class FetcherService {
	constructor(
        private http: HttpClient,
    ) {	}
    public presets: any = {
		text: {
			headers: new HttpHeaders().set('Accept', 'text/plain'),
			responseType: 'text',
			observe: 'body',
            withCredentials: true
		},
		json: {
			headers: new HttpHeaders().set('Accept', 'Application/json'),
			responseType: 'json',
		},
		png: {
			responseType: 'arraybuffer',
			headers: new HttpHeaders().set('Accept', 'Image/png'),
		}
	}
    public fetch (url:string, options?:any):Observable<any> {
		let request = this.http.get(url, options).pipe(catchError(this.fetchError));
		// request.pipe(
		// 	tap(thing => {
		// 		console.log(thing)
		// 	})
		// )
		return request;
	}
    private fetchError = (error: HttpErrorResponse) => { return throwError(error); };
}
