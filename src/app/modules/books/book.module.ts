import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BookService } from  './book.service';
import { BooksComponent } from './components';
import { MaterialModule } from '../material/material.module';

@NgModule({
	declarations: [
		BooksComponent
	],
	exports: [],
	imports: [
		CommonModule,
		MaterialModule
	],
	providers: [
		BookService
	]
})
export class BookModule { }
