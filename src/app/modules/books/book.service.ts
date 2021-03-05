import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from './book';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
@Injectable({
  providedIn: 'root'
})
export class BookService {
	public books: BehaviorSubject<Book[]> = new BehaviorSubject(null);
	private apiRoute: string = "http://localhost:3000/books";
	constructor(
		private http: HttpClient
	) {
        this.read().subscribe(
            (books) => this.books.next(books),
            console.error
        )
	}
	private request(method: string, url: string, data?: any):Observable<any> {
		return this.http.request(method, url, {
			body: data,
			responseType: 'json',
			observe: 'body',
		});
	}
	public create = (book:Book) => this.request('post', this.apiRoute, book)
	public read = (book?:Book) => this.request('get', (book) ? `${this.apiRoute}/${book.id}` : this.apiRoute);
	public update = (book:Book) => this.request('post', `${this.apiRoute}/${book.id}`, book).pipe(
		tap(books => {
			console.error(books);
		})
	)
	public delete = (book:Book) => this.request('delete', `${this.apiRoute}/${book.id}`);
}