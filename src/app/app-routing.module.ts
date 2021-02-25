import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AddApiComponent } from './components/apis/add-api/add-api.component';
import { EditApiComponent } from './components/apis/edit-api/edit-api.component';
import { ApisComponent } from './components/apis/apis.component';
import { AppComponent } from './app.component';
export const routes: Routes = [
	{ path: '', pathMatch: 'full', redirectTo: 'home' },
	{ path: 'home', component: AppComponent },
	{ path: 'add-api', component: AddApiComponent },
	{ path: 'edit-api/:id', component: EditApiComponent },
	{ path: 'apis', component: ApisComponent }
];
@NgModule({
	declarations: [],
	imports: [RouterModule.forRoot(routes)],
	exports: [
		RouterModule
	]
})
export class AppRoutingModule { }