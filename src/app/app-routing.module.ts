import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AddBookComponent } from '@modules/books/components/add-book/add-book.component';
import { EditBookComponent } from '@modules/books/components/edit-book/edit-book.component';
import { BooksComponent } from '@modules/books/components/books.component';
export const routes: Routes = [
	{ path: '', pathMatch: 'full', redirectTo: 'books' },
	{ path: 'add-book', component: AddBookComponent },
	{ path: 'edit-book/:id', component: EditBookComponent },
	{ path: 'books', component: BooksComponent }
];
@NgModule({
	declarations: [],
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule]
})
export class AppRoutingModule { }