import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { LoggerService } from './logger.service';
@Injectable({
	providedIn: 'root'
})
export class ApiService {
	public apis:  Object = {};
	public books: any = {};
	public presets: any = {
		text: {
			headers: new HttpHeaders().set('Accept', 'text/plain'),
			responseType: 'text',
		},
		json: {
			headers: new HttpHeaders().set('Accept', 'Application/json'),
			responseType: 'json',
		}
	}
	constructor(
		private logger: LoggerService,
		private http: HttpClient,
	) {	}
	public init = this.initialize;
	private async initialize() {
		this.logger.log(`Initializing ${this.constructor.name}...`);
		// await this.getApis().pipe(tap(apis => {
		// 	apis.forEach(api => (this.apis[api.name] = this.getApi(api.url, api.options)));
		// })).subscribe();
		this.getBooks()
			.pipe(tap(books => {
				books.forEach(book => {
					this.books[book.name] = { title: book.name };
					this.logger.log(`Getting '${book.name}'...`);
					this.books[book.name].get = this.getApi(book.url, book.options).pipe(map(this.trimGutenbergBookSpacing.bind(this)));
				});
			})).subscribe();
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
	private getBooks(): Observable<any[]> {
		// @TODO: Replace this function with a looker upper
		let books: Object[] = [
			{
				name: 'The Mysterious Island',
				url: "https://www.gutenberg.org/files/1268/1268-0.txt",
				options: {
					... this.presets.text,
					... { observe: 'body' }
				}
			},
			// {
			// 	name: '2 B R 0 2 B',
			// 	url: 'https://www.gutenberg.org/cache/epub/21279/pg21279.txt',
			// 	options: {
			// 		... this.presets.text,
			// 		... { observe: 'body' }
			// 	}
			// },
			// {
			// 	name: 'The Time Machine',
			// 	url: 'https://www.gutenberg.org/files/35/35-0.txt',
			// 	options: {
			// 		... this.presets.text,
			// 		... { observe: 'body' }
			// 	}
			// }
		];
		return of(books);
	}
	private trimGutenbergBookSpacing(gutenberg) {
		this.logger.log(`Trimming whitespace from gutenberg book...`);
		let tab = `\\t`, space = '\\s', nonSpace = '\\S', newline = `[\\r\\n]`,
			trailingSpace = `[${tab}]*${newline}+[${tab}]*`,
			splats = '[\\*]{3}';
		let startRegex = `(${newline}${splats} START .*${splats}${trailingSpace})`,
			endRegex = `${newline}End of the Project Gutenberg EBook of .+${newline}`,
			contentRegex = new RegExp(`(${startRegex}(.[${space}${nonSpace}]*)${endRegex})`, 'g'),
			eightyCharLineRegex = new RegExp(`(${nonSpace}).${newline}{1}(${nonSpace})`, 'gs');
		let contents = contentRegex.exec(gutenberg);
		return (contents) ? contents[3].replace(eightyCharLineRegex, '') : gutenberg;
	}
	public getApi = (url:string, options?:any) => this.http.get(url, options).pipe(catchError(this.apiError));
	private apiError = (error: HttpErrorResponse) => { console.error(error); return throwError(error); };
}
