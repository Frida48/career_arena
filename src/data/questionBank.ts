import type { BankQuestion } from '../types';
import { BANK_QUESTIONS, getBankQuestion } from './questions';

/**
 * Sual bankı (9–11-ci siniflər). Suallar src/data/questions/*.json fayllarından yüklənir.
 * Backend hazır olanda API ilə əvəz oluna bilər — forma eyni qalır.
 */
export const QUESTION_BANK: BankQuestion[] = BANK_QUESTIONS;

export const getQuestion = (id: number) => getBankQuestion(id);
