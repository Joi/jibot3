import { MigrationInterface, QueryRunner, Table } from "typeorm";

export class CreateOptionsTable1615248481055 implements MigrationInterface {
    public async up(queryRunner: QueryRunner): Promise<void> {
		return await queryRunner.createTable(new Table({
            name: "options",
            columns: [
                {
                    name: "id",
                    type: "integer",
                    isPrimary: true,
                    isGenerated: true,
                    generationStrategy: 'increment'
                },
                {
                    name: "name",
                    type: "text",
                    isNullable: false,
                },
                {
                    name: "value",
                    type: "text",
                    isNullable: false
                },
            ]
        }), true);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
		return await queryRunner.dropTable("options");
    }

}
