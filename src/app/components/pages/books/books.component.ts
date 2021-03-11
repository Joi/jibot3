import { Component, OnDestroy, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { Book } from '@modules/server/books/book';
import { BookService } from '@modules/server/books/book.service';
import { EditBookComponent } from './edit-book/edit-book.component';

@Component({
	selector: 'app-books',
	templateUrl: './books.component.html',
	styleUrls: ['./books.component.scss'],
})
export class BooksComponent implements OnInit, OnDestroy {
    public books: BehaviorSubject<Book[]> = new BehaviorSubject(null);
    public displayedColumns = ["id", "title", "url", "actions"];
	public tableDataSource;
  	private subscriber;
    private subscribers = {};
	constructor(
		private bookService: BookService,
		public matDialog: MatDialog,
	) {
        this.subscriber = this.bookService.read().subscribe((books:Book[]) => this.books.next(books));
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
		this.books.subscribe(books => this.tableDataSource = books);
    }
	ngOnDestroy(): void {
        if (this.subscriber?.unsubscribe) this.subscriber.unsubscribe();
        Object.keys(this.subscribers).forEach(id => this.subscribers[id].unsubscribe());
    }
}