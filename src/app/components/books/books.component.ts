import { Component, OnInit } from '@angular/core';
import { Book } from '@app/modules/books/book';
import { BookService } from '@modules/books/book.service';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.scss']
})
export class BooksComponent implements OnInit {
	public books: Book[];
	constructor(
		private bookService: BookService,
	) {
	}

	ngOnInit(): void {
		this.getBooks().then

	}

	private getBooks() {
		return this.bookService.read()
			.then(sub => sub.subscribe(
				(res:Book[]) => this.books = res,
				console.error
			)).catch(console.error)
	}
}
