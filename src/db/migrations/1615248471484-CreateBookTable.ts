import { MigrationInterface, QueryRunner, Table } from "typeorm";

export class CreateBookTable1615248471484 implements MigrationInterface {
    public async up(queryRunner: QueryRunner,): Promise<void> {
		await queryRunner.createTable(new Table({
            name: "books",
            columns: [
                {
                    name: "id",
                    type: "integer",
                    isPrimary: true,
                    isGenerated: true,
                    generationStrategy: 'increment'
                },
                {
                    name: "title",
                    type: "text",
                    isNullable: false,
                },
                {
                    name: "url",
                    type: "text",
                    isNullable: false
                },
                {
                    name: "content",
                    type: "text",
                    isNullable: true
                }
            ]
        }), true);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
		return await queryRunner.dropTable("books");
    }

}
