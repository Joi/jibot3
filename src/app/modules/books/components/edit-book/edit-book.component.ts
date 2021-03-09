import { Component, Input, Output, EventEmitter, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { DialogService } from '@app/services/dialog.service';
import { Book } from '../../book';
import { BookService } from '../../book.service';
@Component({
  selector: 'app-edit-book',
  templateUrl: './edit-book.component.html',
  styleUrls: ['./edit-book.component.scss']
})
export class EditBookComponent implements OnInit {
	@Input() book: Book;
	@Output() bookChanged:EventEmitter<Book[]> = new EventEmitter<Book[]>();
	public action: string = "update";
    public formGroup: FormGroup;
	constructor(
		private formBuilder: FormBuilder,
		private bookService: BookService,
		private dialogService: DialogService,
	) {	}
	ngOnInit(): void {
		if (!this.book) {
			this.book = new Book();
			this.action = "create";
		}
		this.formGroup = this.formBuilder.group(this.book);
	}
	public create(book:Book) {
		this.bookService.create(book).subscribe(
            (books) => {
				this.dialogService.close('new-book', books);
			},
            console.error
        );
    }
	public update(book:Book) {
		this.bookService.update(book).subscribe(
            (books) => this.bookChanged.emit(books),
            console.error
        );
    }
	public delete (book:Book) {
		this.bookService.delete(book).subscribe(
            (books) => this.bookChanged.emit(books),
            console.error
        );
    }
}
