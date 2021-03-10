import { Component, OnDestroy, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { Book } from '@app/modules/books/book';
import { EditBookComponent } from './edit-book/edit-book.component';
import { BookService } from '../book.service';

@Component({
	selector: 'app-books',
	templateUrl: './books.component.html',
	styleUrls: ['./books.component.scss'],
})
export class BooksComponent implements OnInit, OnDestroy {
    public books: BehaviorSubject<Book[]> = new BehaviorSubject(null);
	public displayedColumns: string[] = Object.keys(new Book());
	public tableDataSource;
  	private subscriber;
    private subscribers = {};
	private dialog;
	constructor(
		private bookService: BookService,
		public matDialog: MatDialog,
	) {
	}
	public openDialog() {
		this.matDialog.open(EditBookComponent)
            .afterClosed()
            .subscribe((books:Book[]) => this.books.next(books));
	}
	public onBookChanged(books):void {
		this.books.next(books);
	};
    ngOnInit(): void {
		this.subscriber = this.bookService.read().subscribe((books:Book[]) => this.books.next(books));
		this.books.subscribe(books => this.tableDataSource = books);
    }
	ngOnDestroy(): void {
        this.subscriber.unsubscribe();
        Object.keys(this.subscribers).forEach(id => this.subscribers[id].unsubscribe());
    }
}
