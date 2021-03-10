import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Book } from '@modules/server/books/book';
import { BookService } from '@modules/server/books/book.service';
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
		public dialogRef: MatDialogRef<EditBookComponent>,
	) {	}
	ngOnInit(): void {
		if (!this.book) {
			this.book = new Book();
			this.action = "create";
		}
		this.formGroup = this.formBuilder.group(this.book);
		this.formGroup.controls.url.setValidators(Validators.pattern('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?'));
	}
	public create(book:Book) {
		this.bookService.getContent(book).subscribe(content => {
			book.content = content;
			this.bookService.create(book).subscribe(books => {
				this.dialogRef.close(books);
			})
		});
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
