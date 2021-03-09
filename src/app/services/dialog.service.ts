import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

@Injectable({
 	 providedIn: 'root'
})
export class DialogService {
	private dialogs: any[] = [];
  	constructor(
		public dialog: MatDialog
	) { }
	add(modal: any) {
		this.dialogs.push(modal);
    }
    remove(id: string) {
        this.dialogs = this.dialogs.filter(x => x.id !== id);
    }
    open(id: string, data?:any) {
        let modal: any = this.dialogs.filter(x => x.id === id)[0];
		if (data) modal.open(data);
        else modal.open();
    }
    close(id: string, data?:any) {
		console.log(this.dialogs);
		// let modal: any = this.dialogs.filter(x => x.id === id)[0];
		// if (data) modal.close(data);
	    // else modal.close();
    }
}
