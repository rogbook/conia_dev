declare module 'PermissionInfoModule' {
  export interface AvailablePermission {
    category: string | null;
    code: string;
    description: string;
    group: string | null;
    name: string;
    type: string;
  }
  export interface Permission {
    permission_code: string;
    name: string;
    target: string;
    exclude: string | null;
  }

  export interface Class {
    class_code: string;
    permissions: Permission[];
  }

  export interface PermissionInfo {
    Class: Class[];
    Member: Permission[];
  }
}
