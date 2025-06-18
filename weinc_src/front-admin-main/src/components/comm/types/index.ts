export interface IItem {
  id?: number;
  folder: boolean;
  name: string;
  parent: string | null;
}
export interface IFileSystem {
  items: IItem[];
  nextFolderId: number;
}
