import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BookService } from  './book.service';

@NgModule({
	declarations: [],
	exports: [],
	imports: [
		CommonModule
	],
	providers: [
		BookService
	]
})
export class BookModule { }
