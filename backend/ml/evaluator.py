"""
Model Evaluator
Evaluate ML models with realistic metrics
"""
import numpy as np
import pandas as pd
from sklearn.metrics import (
    confusion_matrix, classification_report,
    roc_curve, auc, precision_recall_curve
)
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from data.telemetry_generator import TelemetryGenerator
from data.attack_simulator import AttackSimulator
from ml.detector import EnsembleDetector


class ModelEvaluator:
    """Evaluate detection models with realistic metrics"""
    
    def __init__(self):
        self.detector = EnsembleDetector()
        self.telemetry_gen = TelemetryGenerator(num_endpoints=settings.NUM_ENDPOINTS)
        self.attack_sim = AttackSimulator(self.telemetry_gen)
    
    def generate_test_dataset(self, num_normal: int = 500, 
                            num_attacks: int = 100) -> tuple[pd.DataFrame, np.ndarray]:
        """Generate test dataset with labels"""
        # Generate mixed data
        dataset = self.attack_sim.generate_mixed_dataset(num_normal, num_attacks)
        
        # Extract features and labels
        X = dataset[settings.FEATURES].values
        y = dataset["is_attack"].values.astype(int)
        
        return dataset, y
    
    def evaluate(self, num_normal: int = 1000, num_attacks: int = 200):
        """
        Comprehensive model evaluation
        
        Args:
            num_normal: Number of normal samples
            num_attacks: Number of attack samples
            
        Returns:
            Dictionary with evaluation metrics
        """
        print("=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)
        
        # Load models
        self.detector.load_models()
        
        # Generate test data
        print(f"\nGenerating test dataset...")
        print(f"  Normal samples: {num_normal}")
        print(f"  Attack samples: {num_attacks}")
        
        dataset, y_true = self.generate_test_dataset(num_normal, num_attacks)
        X = dataset[settings.FEATURES].values
        
        print(f"  Total samples: {len(X)}")
        
        # Predict
        print("\nRunning detection...")
        results = self.detector.detect(X, apply_realism=True)
        
        # Extract predictions
        y_pred = np.array([1 if r.is_anomaly else 0 for r in results])
        scores = np.array([r.ensemble_score for r in results])
        
        # Calculate metrics
        metrics = self._calculate_metrics(y_true, y_pred, scores)
        
        # Print results
        self._print_results(metrics)
        
        # Generate plots
        self._generate_plots(y_true, y_pred, scores, metrics)
        
        return metrics
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                          scores: np.ndarray) -> dict:
        """Calculate all evaluation metrics"""
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        # Basic metrics
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else 0
        false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        # ROC-AUC
        fpr, tpr, _ = roc_curve(y_true, scores)
        roc_auc = auc(fpr, tpr)
        
        # PR-AUC
        precision_curve, recall_curve, _ = precision_recall_curve(y_true, scores)
        pr_auc = auc(recall_curve, precision_curve)
        
        return {
            "confusion_matrix": cm,
            "true_positives": int(tp),
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "false_positive_rate": false_positive_rate,
            "false_negative_rate": false_negative_rate,
            "roc_auc": roc_auc,
            "pr_auc": pr_auc,
            "roc_curve": (fpr, tpr),
            "pr_curve": (precision_curve, recall_curve)
        }
    
    def _print_results(self, metrics: dict):
        """Print evaluation results"""
        print("\n" + "=" * 60)
        print("EVALUATION RESULTS")
        print("=" * 60)
        
        print("\nConfusion Matrix:")
        print(f"  True Positives:  {metrics['true_positives']:>6}")
        print(f"  True Negatives:  {metrics['true_negatives']:>6}")
        print(f"  False Positives: {metrics['false_positives']:>6}")
        print(f"  False Negatives: {metrics['false_negatives']:>6}")
        
        print("\nPerformance Metrics:")
        print(f"  Accuracy:         {metrics['accuracy']:.2%}")
        print(f"  Precision:        {metrics['precision']:.2%}")
        print(f"  Recall:           {metrics['recall']:.2%}")
        print(f"  F1 Score:         {metrics['f1_score']:.2%}")
        print(f"  ROC-AUC:          {metrics['roc_auc']:.2%}")
        print(f"  PR-AUC:           {metrics['pr_auc']:.2%}")
        
        print("\nError Rates:")
        print(f"  False Positive Rate: {metrics['false_positive_rate']:.2%}")
        print(f"  False Negative Rate: {metrics['false_negative_rate']:.2%}")
        
        print("\n" + "=" * 60)
    
    def _generate_plots(self, y_true: np.ndarray, y_pred: np.ndarray, 
                       scores: np.ndarray, metrics: dict):
        """Generate evaluation plots"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle('Model Evaluation Results', fontsize=16)
        
        # Confusion Matrix
        ax = axes[0, 0]
        cm = metrics['confusion_matrix']
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)
        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               xticklabels=['Normal', 'Attack'],
               yticklabels=['Normal', 'Attack'],
               title='Confusion Matrix',
               ylabel='True Label',
               xlabel='Predicted Label')
        
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                       ha="center", va="center",
                       color="white" if cm[i, j] > cm.max() / 2 else "black")
        
        # ROC Curve
        ax = axes[0, 1]
        fpr, tpr = metrics['roc_curve']
        ax.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {metrics["roc_auc"]:.2f})')
        ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curve')
        ax.legend(loc="lower right")
        ax.grid(True, alpha=0.3)
        
        # Precision-Recall Curve
        ax = axes[1, 0]
        precision_curve, recall_curve = metrics['pr_curve']
        ax.plot(recall_curve, precision_curve, color='purple', lw=2,
                label=f'PR curve (AUC = {metrics["pr_auc"]:.2f})')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_title('Precision-Recall Curve')
        ax.legend(loc="lower left")
        ax.grid(True, alpha=0.3)
        
        # Score Distribution
        ax = axes[1, 1]
        ax.hist(scores[y_true == 0], bins=30, alpha=0.5, label='Normal', color='blue')
        ax.hist(scores[y_true == 1], bins=30, alpha=0.5, label='Attack', color='red')
        ax.set_xlabel('Anomaly Score')
        ax.set_ylabel('Frequency')
        ax.set_title('Score Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(settings.BASE_DIR, 'evaluation_results.png')
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        print(f"\nEvaluation plots saved to: {plot_path}")


if __name__ == "__main__":
    evaluator = ModelEvaluator()
    
    try:
        metrics = evaluator.evaluate(num_normal=1000, num_attacks=200)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure models are trained first (run trainer.py)")
