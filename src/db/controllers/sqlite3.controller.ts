
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
    private getRepoFromRequest(request:Request) {
        let entityName = request.route.path.replace("/","").toLowerCase();
        return this.repositories[entityName];
    }
	async all(request: Request, response: Response, next: NextFunction) {
		let repo = this.getRepoFromRequest(request);
		return repo.find();
    }
    async one(request: Request, response: Response, next: NextFunction) {
		let repo = this.getRepoFromRequest(request);
        return repo.findOne(request.params.id);
    }
    async save(request: Request, response: Response, next: NextFunction) {
        let repo = this.getRepoFromRequest(request);
		await repo.save(request.body);
		return repo.find();
    }
    async remove(request: Request, response: Response, next: NextFunction) {
		let repo = this.getRepoFromRequest(request);
        const itemToRemove = await repo.findOne(request.params.id);
        await repo.remove(itemToRemove);
		return repo.find();
    }
}