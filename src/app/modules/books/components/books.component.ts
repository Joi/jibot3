import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Book } from '@app/modules/books/book';
import { BookService } from '@modules/books/book.service';
import { BehaviorSubject, Observable, Subscriber } from 'rxjs';
@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.scss']
})
export class BooksComponent implements OnInit, OnDestroy {
    public books = this.bookService.books;
    private subscriber;
	constructor(
		private bookService: BookService,
	) { }
    ngOnInit(): void {
        this.subscriber = this.books.subscribe(console.log);
    }
	ngOnDestroy(): void {
        this.subscriber.unsubscribe();
    }
    public delete = (book:Book) => {
        this.bookService.delete(book).subscribe(
            (r) => {
                console.log(r);
                console.log("DELETED");
            },
            console.error
        );
    }
}
