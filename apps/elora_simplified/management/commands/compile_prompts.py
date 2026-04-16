#!/usr/bin/env python3
"""
Management command to compile modular prompts into monolithic files.

Useful for debugging, distribution, and backup purposes.
"""

from pathlib import Path
from django.core.management.base import BaseCommand, CommandError

from ...prompts.prompt_builder import PromptBuilder


class Command(BaseCommand):
    help = 'Compile modular prompt system into monolithic files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default=None,
            help='Output directory for compiled prompts (default: prompts/compiled)'
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate modules without generating output'
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show detailed module statistics'
        )

    def handle(self, *args, **options):
        """Main command handler."""
        prompts_dir = Path(__file__).parent.parent.parent / "prompts"

        if not prompts_dir.exists():
            raise CommandError(f"Prompts directory not found: {prompts_dir}")

        builder = PromptBuilder(prompts_dir)

        # Validate modules first
        self.stdout.write("🔍 Validating modular prompt system...")
        validation = builder.validate_modules()

        if not validation["valid"]:
            self.stdout.write(
                self.style.ERROR("❌ Validation failed:")
            )
            for issue in validation["issues"]:
                self.stdout.write(f"  • {issue}")
            return

        self.stdout.write(
            self.style.SUCCESS("✅ All modules validated successfully")
        )

        # Show statistics if requested
        if options['stats']:
            stats = validation["statistics"]
            self.stdout.write("\n📊 Module Statistics:")
            self.stdout.write(f"  • Total files: {stats['total_files']}")
            self.stdout.write(f"  • Total characters: {stats['total_characters']:,}")
            self.stdout.write(f"  • Estimated tokens: {stats['estimated_tokens']:,}")
            self.stdout.write(f"  • Categories: {stats['categories']}")

            self.stdout.write("\n📁 Modules by category:")
            modules = builder.list_modules()
            for category, module_list in modules.items():
                self.stdout.write(f"  • {category}: {len(module_list)} modules")
                for module in module_list:
                    self.stdout.write(f"    - {module}")

        # Exit if validation-only
        if options['validate_only']:
            return

        # Compile prompts
        self.stdout.write("\n🔧 Compiling modular prompts...")

        try:
            compiled_prompt = builder.load_all_modules()

            # Determine output directory
            if options['output_dir']:
                output_dir = Path(options['output_dir'])
            else:
                output_dir = prompts_dir / "compiled"

            output_dir.mkdir(exist_ok=True)

            # Write compiled prompt
            output_file = output_dir / "system_prompt_compiled.txt"
            output_file.write_text(compiled_prompt, encoding='utf-8')

            self.stdout.write(
                self.style.SUCCESS(f"✅ Compiled prompt written to: {output_file}")
            )
            self.stdout.write(f"📊 Size: {len(compiled_prompt):,} characters")

        except Exception as e:
            raise CommandError(f"Failed to compile prompts: {e}")