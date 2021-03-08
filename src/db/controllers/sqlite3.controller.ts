
import { getRepository } from "typeorm";
import { NextFunction, Request, Response } from "express";
import * as Entities from "../entities";
export class Sqlite3Controller {
	private repositories = {};
	constructor() {
		Object.keys(Entities).forEach(name => {
			this.repositories[name.toLowerCase()] = getRepository(Entities[name]);
		});
	}
	async all(request: Request, response: Response, next: NextFunction) {
		let repo = this.repositories[request.route.path.replace("/", "")];
		console.log(request.route.path.replace("/", ""));
		repo.find().then(console.log);
		return repo.find();
    }
    async one(request: Request, response: Response, next: NextFunction) {
		let repo = this.repositories[request.route.path.replace("/", "")];
        return repo.findOne(request.params.id);
    }
    async save(request: Request, response: Response, next: NextFunction) {
		let repo = this.repositories[request.route.path.replace("/", "")];
		await repo.save(request.body);
		return repo.find();
    }
    async remove(request: Request, response: Response, next: NextFunction) {
		let repo = this.repositories[request.route.path.replace("/", "")];
        const bookToRemove = await repo.findOne(request.params.id);
        await repo.remove(bookToRemove);
		return repo.find();
    }
}