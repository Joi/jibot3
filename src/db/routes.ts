import { Sqlite3Controller } from "./controllers/sqlite3.controller";
import * as Entities from './entities';
export let Routes = [];
Object.keys(Entities).forEach(entityName => {
	// Import all the entities present, and loop through to set up the db routes
	let route = "/" + entityName.toLowerCase();
	let entityRoutes = [
        {
			method: "get",
			route: `${route}`,
			controller: Sqlite3Controller,
			action: "all"
		}, {
			method: "get",
			route: `${route}/:id`,
			controller: Sqlite3Controller,
			action: "one"
		}, {
			method: "put",
			route: `${route}/:id`,
			controller: Sqlite3Controller,
			action: "save",
		}, {
            method: "post",
			route: `${route}`,
			controller: Sqlite3Controller,
			action: "save",
        }, {
			method: "delete",
			route: `${route}/:id`,
			controller: Sqlite3Controller,
			action: "remove"
		}
	];
	Routes = [...Routes, ...entityRoutes];
});