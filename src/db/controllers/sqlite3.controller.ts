
import { getRepository } from "typeorm";
import { NextFunction, Request, Response } from "express";
import * as Entities from "../entities";
export class Sqlite3Controller {
	private repositories = {};
    constructor() {
		this.saveEntityRepos();
	}
	async all(request: Request, response: Response, next: NextFunction) {
		let repo = this.getRepoFromRequest(request);
		if (repo) return repo.find();
    }
    async one(request: Request, response: Response, next: NextFunction) {
		let repo = this.getRepoFromRequest(request);
		if (repo) return repo.findOne(request.params.id);

    }
    async save(request: Request, response: Response, next: NextFunction) {
        let repo = this.getRepoFromRequest(request);
		if (repo) {
			await repo.save(request.body);
			return repo.find();
		}
    }
    async remove(request: Request, response: Response, next: NextFunction) {
		let repo = this.getRepoFromRequest(request);
		if (repo) {
			const itemToRemove = await repo.findOne(request.params.id);
			await repo.remove(itemToRemove);
			return repo.find();
		}
    }
	private saveEntityRepos() {
		Object.keys(Entities).forEach(name => {
			if (Entities[name]) {
				this.repositories[name.toLowerCase()] = getRepository(Entities[name])
			}
		});
	}
    private getRepoFromRequest(request:Request) {
		let repo;
		let preceedingSlash = /(^\/)/;
		let entityName = request.route.path.replace(preceedingSlash, "").split("/")[0];
		try {
			repo = this.repositories[entityName];
		} catch(e) {
			console.error(e)
		}
		return repo;
    }
}