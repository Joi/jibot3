import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Book } from '@app/modules/books/book';
import { BookService } from '@modules/books/book.service';
import { Observable, Subscription } from 'rxjs';
@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.scss']
})
export class BooksComponent implements OnInit, OnDestroy {
	private subscription;
	public books: Book[];
	constructor(
		private bookService: BookService,
	) {
		//this.bookService.read().then((s) => this.subscription = s);
	}
	ngOnInit(): void {
		//this.subscription.subscribe((books:Book[]) => this.books = books);
	}
	ngOnDestroy(): void {
		//this.subscription.uns
	}
}
