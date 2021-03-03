import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from './book';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class BookService {
	public books:Book[];
	private apiRoute: string = "http://localhost:3000/books";
	constructor(
		private http: HttpClient
	) {
	}
	private async request(method: string, url: string, data?: any):Promise<Observable<Object>> {
		return this.http.request(method, url, {
			body: data,
			responseType: 'json',
			observe: 'body',
		});
	}
	private create = (book:Book) => this.request('post', this.apiRoute, book)
	//public read = (book?:Book) => this.request('get', (book) ? `${this.apiRoute}/${book.id}` : this.apiRoute);
	private update = (book:Book) => this.request('post', `${this.apiRoute}${book.id}`, book);
	private destroy = (book:Book) => this.request('delete', `${this.apiRoute}${book.id}`);

	public read = (book?:Book) => {

		return this.request('get', (book) ? `${this.apiRoute}${book.id}` : this.apiRoute);
	}
}