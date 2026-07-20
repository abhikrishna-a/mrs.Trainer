import { Role } from '../types/api'

interface CategoryTabsProps {
  roles: Role[]
  activeRole: string | null
  onSelect: (slug: string | null) => void
}

export default function CategoryTabs({ roles, activeRole, onSelect }: CategoryTabsProps) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-none">
      <button
        onClick={() => onSelect(null)}
        className={`shrink-0 px-4 py-2 rounded-full text-sm font-semibold transition-all cursor-pointer ${
          !activeRole
            ? 'bg-accent-red-soft text-white shadow-lg shadow-accent-red-soft/20'
            : 'bg-bg-surface text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover'
        }`}
      >
        All
      </button>
      {roles.map((role) => (
        <button
          key={role.slug}
          onClick={() => onSelect(role.slug)}
          className={`shrink-0 px-4 py-2 rounded-full text-sm font-semibold transition-all cursor-pointer ${
            activeRole === role.slug
              ? 'bg-accent-red-soft text-white shadow-lg shadow-accent-red-soft/20'
              : 'bg-bg-surface text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover'
          }`}
        >
          {role.name}
        </button>
      ))}
    </div>
  )
}
