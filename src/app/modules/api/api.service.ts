import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { LoggerService } from '@services/logger.service';
@Injectable({
	providedIn: 'root'
})
export class ApiService {
	constructor(
		private logger: LoggerService,
		private http: HttpClient,
	) {	}
	public apis:  Object = {};
	public books: any = {};
	public presets: any = {
		text: {
			headers: new HttpHeaders().set('Accept', 'text/plain'),
			responseType: 'text',
			observe: 'body'
		},
		json: {
			headers: new HttpHeaders().set('Accept', 'Application/json'),
			responseType: 'json',
		}
	}
	public async init () {
		this.logger.log(`Initializing ${this.constructor.name}...`);
		await this.getApis()
			.pipe(
				tap(apis => apis.forEach(api => (this.apis[api.name] = this.get(api.url, api.options))))
			).subscribe(
				response => {
					Object.keys(this.apis).forEach(i => {
						let api = this.apis[i];
						api.subscribe(
							console.log, this.logger.error
						)
					});
				},
				this.logger.error
			);
		return;
	}
	private getApis(): Observable<any[]> {
		// @TODO: Replace this function with a looker upper
		let apis: Object[] = [
			{
				name: 'Montgomery County Maryland Adoptable Animals',
				url: "https://data.montgomerycountymd.gov/resource/e54u-qx42.json",
				options: {
					... this.presets.json,
					... {
						params: new HttpParams().set('$$app_token', 'PmYY236OzmufmnCoMwT7Pgpkb')
					}
				}
			}
		];
		return of(apis);
	}

	public get = (url:string, options?:any) => this.http.get(url, options).pipe(catchError(this.apiError));
	private apiError = (error: HttpErrorResponse) => { console.error(error); return throwError(error); };
}
