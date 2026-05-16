import React from 'react';
import { cn } from '@/lib/utils/cn';

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
  children: React.ReactNode;
}

export const Badge = React.forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant = 'default', children, ...props }, ref) => {
    const variants = {
      default: 'bg-slate-700/50 text-slate-300 border-slate-600',
      success: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
      warning: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
      error: 'bg-red-500/10 text-red-400 border-red-500/30',
      info: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium backdrop-blur-sm',
          variants[variant],
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Badge.displayName = 'Badge';

// Made with Bob
