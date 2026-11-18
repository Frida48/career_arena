import React from 'react';
import type { Grade } from '../types';
import { GRADES, gradeLabel } from '../data/questions';
import { useExam } from '../context/ExamContext';

/** Sinif seçimi (9 / 10 / 11). Sinif dəyişəndə bölmə və mövzu seçimi sıfırlanır. */
export const GradePicker: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { setup, updateSetup } = useExam();
  const choose = (grade: Grade) => updateSetup({ grade, sectionId: undefined, topicIds: [] });

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <span className="text-xs font-bold uppercase tracking-wider text-stone-500 dark:text-stone-400">
        Sinif
      </span>
      <div
        role="radiogroup"
        aria-label="Sinif"
        className="inline-flex p-1 rounded-full bg-stone-100 dark:bg-inset-dark border border-stone-200 dark:border-stone-800"
      >
        {GRADES.map((g) => {
          const active = setup.grade === g;
          return (
            <button
              key={g}
              role="radio"
              aria-checked={active}
              onClick={() => choose(g)}
              className={`h-8 px-4 rounded-full text-sm font-semibold transition-colors ${
                active
                  ? 'bg-brand text-white dark:bg-brand-400 dark:text-ink'
                  : 'text-stone-600 dark:text-stone-300 hover:text-brand-fg'
              }`}
            >
              {gradeLabel(g)}
            </button>
          );
        })}
      </div>
    </div>
  );
};
