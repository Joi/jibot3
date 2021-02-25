import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { AddApiComponent } from './components/apis/add-api/add-api.component';
import { EditApiComponent } from './components/apis/edit-api/edit-api.component';
import { ApisComponent } from './components/apis/apis.component';
@NgModule({
	declarations: [
		AppComponent,
		AddApiComponent,
		EditApiComponent,
		ApisComponent
	],
	imports: [
		BrowserModule.withServerTransition({ appId: 'jibot3' }),
		AppRoutingModule
	],
	providers: [],
	bootstrap: [
		AppComponent
	]
})
export class AppModule { }
