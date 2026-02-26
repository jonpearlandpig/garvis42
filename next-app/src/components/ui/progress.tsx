import * as React from "react";
import { cn } from "@/src/utils/utils";

export function Progress({ value = 0, className = "", ...props }: { value?: number } & React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={`w-full h-2 bg-neutral-800 rounded ${className}`} {...props}>
      <div className="h-2 bg-green-500 rounded" style={{ width: `${value}%` }} />
    </div>
  );
}
import * as React from "react";

export function Progress({ value = 0, className = "", ...props }: { value?: number } & React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={`w-full h-2 bg-neutral-800 rounded ${className}`} {...props}>
      <div className="h-2 bg-green-500 rounded" style={{ width: `${value}%` }} />
    </div>
  );
}
