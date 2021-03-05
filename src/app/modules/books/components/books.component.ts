import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Book } from '@app/modules/books/book';
import { BookService } from '@modules/books/book.service';
import { BehaviorSubject } from 'rxjs';
import { EditBookComponent } from './edit-book/edit-book.component';
@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.scss']
})
export class BooksComponent implements OnInit, OnDestroy {
    public books:BehaviorSubject<Book[]> = this.bookService.books;
	public displayedColumns: string[] = Object.keys(new Book());
	public tableDataSource;
  	private subscriber;
	constructor(
		private bookService: BookService,
		public matDialog: MatDialog
	) { }
	public openDialog() {
		let dialog = this.matDialog.open(EditBookComponent);
	}
	public handleChange = (books) => this.books.next(books);
    ngOnInit(): void {
        this.subscriber = this.books.subscribe(books => this.tableDataSource = books);
    }
	ngOnDestroy(): void {
        this.subscriber.unsubscribe();
    }
}
