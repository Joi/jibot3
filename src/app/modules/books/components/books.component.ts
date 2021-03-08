import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

import { MatDialog } from '@angular/material/dialog';
import { Book } from '@app/modules/books/book';
import { EditBookComponent } from './edit-book/edit-book.component';
import { BookService } from '../book.service';

@Component({
	selector: 'app-books',
	templateUrl: './books.component.html',
	styleUrls: ['./books.component.scss'],
	//providers: [{ provide: 'entityName', useValue: 'books' }]
})
export class BooksComponent implements OnInit, OnDestroy {
    public books: BehaviorSubject<Book[]> = new BehaviorSubject(null);
	public displayedColumns: string[] = Object.keys(new Book());
	public tableDataSource;
  	private subscriber;
	constructor(
		private db: BookService,
		public matDialog: MatDialog
	) {
		this.subscriber = this.db.read().subscribe((books:Book[]) => this.books.next(books));
	}
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
