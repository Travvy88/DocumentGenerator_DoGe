import random
from augraphy import * 


def get_augmentation_phases():

    pre_phase = [
        # Rescale(scale="optimal", target_dpi = 300,  p = 1.0),
    ]

    ink_phase = [
        InkColorSwap(
            ink_swap_color="random",
            ink_swap_sequence_number_range=(5, 10),
            ink_swap_min_width_range=(2, 3),
            ink_swap_max_width_range=(100, 120),
            ink_swap_min_height_range=(2, 3),
            ink_swap_max_height_range=(100, 120),
            ink_swap_min_area_range=(10, 20),
            ink_swap_max_area_range=(400, 500),
            p=0.1,
        ),
        LinesDegradation(
            line_roi=(0.0, 0.0, 1.0, 1.0),
            line_gradient_range=(32, 255),
            line_gradient_direction=(0, 2),
            line_split_probability=(0.2, 0.4),
            line_replacement_value=(250, 255),
            line_min_length=(30, 40),
            line_long_to_short_ratio=(5, 7),
            line_replacement_probability=(0.4, 0.5),
            line_replacement_thickness=(1, 3),
            p=0.1,
        ),
        OneOf(
            [
                Dithering(
                    dither=random.choice(["ordered", "floyd-steinberg"]),
                    order=(3, 5),
                ),
                InkBleed(
                    intensity_range=(0.1, 0.2),
                    kernel_size=random.choice([(7, 7), (5, 5), (3, 3)]),
                    severity=(0.4, 0.6),
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                InkShifter(
                   text_shift_scale_range=(18, 27),
                   text_shift_factor_range=(1, 4),
                   text_fade_range=(0, 2),
                   blur_kernel_size=(5, 5),
                   blur_sigma=0,
                   noise_type="random",
                ),
                BleedThrough(
                    intensity_range=(0.1, 0.3),
                    color_range=(32, 224),
                    ksize=(17, 17),
                    sigmaX=1,
                    alpha=random.uniform(0.1, 0.2),
                    offsets=(10, 20),
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                Hollow(
                    hollow_median_kernel_value_range=(71, 101),
                    hollow_min_width_range=(1, 2),
                    hollow_max_width_range=(150, 200),
                    hollow_min_height_range=(1, 2),
                    hollow_max_height_range=(150, 200),
                    hollow_min_area_range=(10, 20),
                    hollow_max_area_range=(2000, 5000),
                    hollow_dilation_kernel_size_range=(1, 2),
                ),
                Letterpress(
                    n_samples=(100, 400),
                    n_clusters=(200, 400),
                    std_range=(500, 3000),
                    value_range=(150, 224),
                    value_threshold_range=(96, 128),
                    blur=1,
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                LowInkRandomLines(
                    count_range=(5, 10),
                    use_consistent_lines=random.choice([True, False]),
                    noise_probability=0.1,
                ),
                LowInkPeriodicLines(
                    count_range=(2, 5),
                    period_range=(16, 32),
                    use_consistent_lines=random.choice([True, False]),
                    noise_probability=0.1,
                ),
            ],
            p=0.1,
        ),
    ]

    paper_phase = [
        PaperFactory(p=0.1),
        ColorPaper(
            hue_range=(0, 255),
            saturation_range=(10, 40),
            p=0.1,
        ),
        OneOf(
            [
                #DelaunayTessellation(
                #    n_points_range=(500, 800),
                #    n_horizontal_points_range=(500, 800),
                #    n_vertical_points_range=(500, 800),
                #    noise_type="random",
                #    color_list="default",
                #    color_list_alternate="default",
                #),
                PatternGenerator(
                    imgx=random.randint(256, 512),
                    imgy=random.randint(256, 512),
                    n_rotation_range=(10, 15),
                    color="random",
                    alpha_range=(0.25, 0.5),
                ),
                #VoronoiTessellation(
                 #   mult_range=(50, 80),
                  #  seed=19829813472,
                  #  num_cells_range=(500, 1000),
                  #  noise_type="random",
                  #  background_value=(200, 255),
                #),
            ],
            p=0.1,
        ),
        WaterMark(
            watermark_word="random",
            watermark_font_size=(10, 15),
            watermark_font_thickness=(20, 25),
            watermark_rotation=(0, 360),
            watermark_location="random",
            watermark_color="random",
            watermark_method="darken",
            p=0.1,
        ),
        OneOf(
            [
                AugmentationSequence(
                    [
                        NoiseTexturize(
                            sigma_range=(3, 10),
                            turbulence_range=(2, 5),
                            texture_width_range=(300, 500),
                            texture_height_range=(300, 500),
                        ),
                        BrightnessTexturize(
                            texturize_range=(0.9, 0.99),
                            deviation=0.03,
                        ),
                    ],
                ),
                AugmentationSequence(
                    [
                        BrightnessTexturize(
                            texturize_range=(0.9, 0.99),
                            deviation=0.03,
                        ),
                        NoiseTexturize(
                            sigma_range=(3, 10),
                            turbulence_range=(2, 5),
                            texture_width_range=(300, 500),
                            texture_height_range=(300, 500),
                        ),
                    ],
                ),
            ],
            p=0.1,
        ),
    ]

    post_phase = [
            ColorShift(
                color_shift_offset_x_range=(3, 5),
                color_shift_offset_y_range=(3, 5),
                color_shift_iterations=(2, 3),
                color_shift_brightness_range=(0.9, 1.1),
                color_shift_gaussian_kernel_range=(3, 3),
                p=0.1,
            ),
        OneOf(
            [
                DirtyDrum(
                    line_width_range=(1, 6),
                    line_concentration=random.uniform(0.05, 0.15),
                    direction=random.randint(0, 2),
                    noise_intensity=random.uniform(0.6, 0.95),
                    noise_value=(64, 224),
                    ksize=random.choice([(3, 3), (5, 5), (7, 7)]),
                    sigmaX=0,
                    p=0.1,
                ),
                DirtyRollers(
                    line_width_range=(2, 32),
                    scanline_type=0,
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                LightingGradient(
                    light_position=None,
                    direction=None,
                    max_brightness=255,
                    min_brightness=0,
                    mode="gaussian",
                    linear_decay_rate=None,
                    transparency=None,
                ),
                Brightness(
                    brightness_range=(0.9, 1.1),
                    min_brightness=0,
                    min_brightness_value=(120, 150),
                ),
                Gamma(
                    gamma_range=(0.9, 1.1),
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                SubtleNoise(
                    subtle_range=random.randint(5, 10),
                ),
                Jpeg(
                    quality_range=(25, 95),
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                Markup(
                    num_lines_range=(2, 7),
                    markup_length_range=(0.5, 1),
                    markup_thickness_range=(1, 2),
                    markup_type=random.choice(["strikethrough", "crossed", "highlight", "underline"]),
                    markup_color="random",
                    single_word_mode=False,
                    repetitions=1,
                ),
                Scribbles(
                    scribbles_type="random",
                    scribbles_location="random",
                    scribbles_size_range=(250, 600),
                    scribbles_count_range=(1, 6),
                    scribbles_thickness_range=(1, 3),
                    scribbles_brightness_change=[32, 64, 128],
                    scribbles_text="random",
                    scribbles_text_font="random",
                    scribbles_text_rotate_range=(0, 360),
                    scribbles_lines_stroke_count_range=(1, 6),
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                #BadPhotoCopy(
                #    noise_mask=None,
                #    noise_type=-1,
                #    noise_side="random",
                #    noise_iteration=(1, 2),
                #    noise_size=(1, 3),
                #    noise_value=(128, 196),
                #    noise_sparsity=(0.3, 0.6),
                #    noise_concentration=(0.1, 0.6),
                #    blur_noise=random.choice([True, False]),
                #    blur_noise_kernel=random.choice([(3, 3), (5, 5), (7, 7)]),
                #    wave_pattern=random.choice([True, False]),
                #    edge_effect=random.choice([True, False]),
                #),
                ShadowCast(
                    shadow_side="random",
                    shadow_vertices_range=(1, 20),
                    shadow_width_range=(0.3, 0.8),
                    shadow_height_range=(0.3, 0.8),
                    shadow_color=(0, 0, 0),
                    shadow_opacity_range=(0.2, 0.9),
                    shadow_iterations_range=(1, 2),
                    shadow_blur_kernel_range=(101, 301),
                ),
                LowLightNoise(
                    num_photons_range=(50, 100),
                    alpha_range=(0.7, 1.0),
                    beta_range=(10, 30),
                    gamma_range=(1, 1.8),
                    bias_range=(20, 40),
                    dark_current_value=1.0,
                    exposure_time=0.2,
                    gain=0.1,
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                NoisyLines(
                    noisy_lines_direction="random",
                    noisy_lines_location="random",
                    noisy_lines_number_range=(5, 20),
                    noisy_lines_color=(0, 0, 0),
                    noisy_lines_thickness_range=(1, 2),
                    noisy_lines_random_noise_intensity_range=(0.01, 0.1),
                    noisy_lines_length_interval_range=(0, 100),
                    noisy_lines_gaussian_kernel_value_range=(3, 5),
                    noisy_lines_overlay_method="ink_to_paper",
                ),
                BindingsAndFasteners(
                    overlay_types="darken",
                    foreground=None,
                    effect_type="random",
                    width_range="random",
                    height_range="random",
                    angle_range=(-30, 30),
                    ntimes=(2, 6),
                    nscales=(0.9, 1.0),
                    edge="random",
                    edge_offset=(10, 50),
                    use_figshare_library=0,
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                Squish(
                    squish_direction="random",
                    squish_location="random",
                    squish_number_range=(5, 10),
                    squish_distance_range=(5, 7),
                    squish_line="random",
                    squish_line_thickness_range=(1, 1),
                ),
                Geometric(
                    fliplr=False,
                    flipud=False,
                    crop=(),
                    rotate_range=(-4, 4),
                    randomize=0,
                    p=1,
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                DotMatrix(
                    dot_matrix_shape="random",
                    dot_matrix_dot_width_range=(3, 3),
                    dot_matrix_dot_height_range=(3, 3),
                    dot_matrix_min_width_range=(1, 2),
                    dot_matrix_max_width_range=(150, 200),
                    dot_matrix_min_height_range=(1, 2),
                    dot_matrix_max_height_range=(150, 200),
                    dot_matrix_min_area_range=(10, 20),
                    dot_matrix_max_area_range=(2000, 5000),
                    dot_matrix_median_kernel_value_range=(128, 255),
                    dot_matrix_gaussian_kernel_value_range=(1, 3),
                    dot_matrix_rotate_value_range=(0, 360),
                ),
                Faxify(
                    scale_range=(0.3, 0.6),
                    monochrome=random.choice([0, 1]),
                    monochrome_method="random",
                    monochrome_arguments={},
                    halftone=random.choice([0, 1]),
                    invert=1,
                    half_kernel_size=random.choice([(1, 1), (2, 2)]),
                    angle=(0, 360),
                    sigma=(1, 3),
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                InkMottling(
                    ink_mottling_alpha_range=(0.2, 0.3),
                    ink_mottling_noise_scale_range=(2, 2),
                    ink_mottling_gaussian_kernel_range=(3, 5),
                ),
                ReflectedLight(
                    reflected_light_smoothness=0.8,
                    reflected_light_internal_radius_range=(0.0, 0.001),
                    reflected_light_external_radius_range=(0.5, 0.8),
                    reflected_light_minor_major_ratio_range=(0.9, 1.0),
                    reflected_light_color=(255, 255, 255),
                    reflected_light_internal_max_brightness_range=(0.75, 0.75),
                    reflected_light_external_max_brightness_range=(0.5, 0.75),
                    reflected_light_location="random",
                    reflected_light_ellipse_angle_range=(0, 360),
                    reflected_light_gaussian_kernel_size_range=(5, 310),
                    p=0.1,
                ),
            ],
            p=0.1,
        ),
        OneOf(
            [
                PageBorder(
                    page_border_width_height="random",
                    page_border_color=(0, 0, 0),
                    page_border_background_color=(0, 0, 0),
                    page_numbers="random",
                    page_rotation_angle_range=(-3, 3),
                    curve_frequency=(2, 8),
                    curve_height=(2, 4),
                    curve_length_one_side=(50, 100),
                    same_page_border=random.choice([0, 1]),
                ),
                #BookBinding(
                #    shadow_radius_range=(30, 100),
                #    curve_range_right=(50, 200),
                #    curve_range_left=(50, 200),
                #    curve_ratio_right=(0.1, 0.3),
                #    curve_ratio_left=(0.1, 0.3),
                #    mirror_range=(1.0, 1.0),
                #    binding_align="random",
                #    binding_pages=(5, 10),
                #    curling_direction=-1,
                #    backdrop_color=(0, 0, 0),
                #    enable_shadow=random.choice([0, 1]),
                #),
                Folding(
                    fold_x=None,
                    fold_deviation=(0, 0),
                    fold_count=random.randint(2, 8),
                    fold_noise=0.01,
                    fold_angle_range=(-360, 360),
                    gradient_width=(0.1, 0.2),
                    gradient_height=(0.01, 0.02),
                    backdrop_color=(0, 0, 0),
                ),
            ],
            p=0.1,
        ),
        # Rescale(scale = "original" , p = 1.0)
    ]
    return {'ink_phase': ink_phase, 
            'paper_phase': paper_phase, 
            'post_phase': post_phase, 
            'pre_phase': pre_phase}
